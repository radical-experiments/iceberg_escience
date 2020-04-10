
import os
import sys
import pty
import time
import errno
import shlex
import select
import signal
import termios

import threading as mt


# --------------------------------------------------------------------
#
_CHUNKSIZE = 1024 * 1024  # default size of each read
_POLLDELAY = 0.01         # seconds in between read attempts
_DEBUG_MAX = 600


# --------------------------------------------------------------------
#
class PTYProcess(object):
    '''
    This class spawns a process, providing that child with pty I/O channels --
    it will maintain stdin, stdout and stderr channels to the child.  I/O
    channels are exposed as file descriptors.  The class also provides
    information on process health.  Example::
    '''

    # ----------------------------------------------------------------
    #
    def __init__(self, command, cfg=None):
        '''
        The class constructor, which runs (execvpe) command in a separately
        forked process.  The new process will inherit the environment of the
        application process.

        :type  command: string or list of strings
        :param command: The given command is what is run as a child, and
                        fed/drained via pty pipes.  If given as string,
                        command is split into an array of strings,
                        using :func:`shlex.split`.
        '''

        if isinstance(command, basestring):
            command = shlex.split(command)

        if not isinstance(command, list):
            raise ValueError('PTYProcess expects string or list command')

        if not command:
            raise ValueError('PTYProcess expects non-empty command')

        self.rlock   = mt.RLock()
        self.command = command  # list of strings too run()

        self.cache   = ''      # data cache
        self.tail    = ''      # tail of data data cache for error messages
        self.child   = None    # the process as created by subprocess.Popen
        self.ptyio   = None    # the process' io channel, from pty.fork()

        self.exit_code        = None  # child died with code (may be revived)
        self.exit_signal      = None  # child kill by signal (may be revived)

        self.initialize()


    # --------------------------------------------------------------------
    #
    def __del__(self):
        '''
        Need to free pty's on destruction, otherwise we might ran out of
        them (see cat /proc/sys/kernel/pty/max)
        '''

        with self.rlock:

            try:
                self.kill()
            except:
                pass


    # ----------------------------------------------------------------------
    #
    def initialize(self):

        with self.rlock:

            # create the child
            self.child, self.child_fd = pty.fork()

            if not self.child:
                # child process
                os.execvpe(self.command[0], self.command, os.environ)

            else:
                # parent
                new    = termios.tcgetattr(self.child_fd)
                new[3] = new[3] & ~termios.ECHO

                termios.tcsetattr(self.child_fd, termios.TCSANOW, new)

                self.parent_in  = self.child_fd
                self.parent_out = self.child_fd


    # --------------------------------------------------------------------
    #
    def kill(self, wstat=None):
        '''
        kill the child, close all I/O channels
        '''

        with self.rlock:

            # now we can safely kill the process
            # (unless some wait did that before)
            if wstat is None:

                if self.child:
                    # yes, we have something to kill!
                    try:
                        os.kill(self.child, signal.SIGKILL)
                    except OSError:
                        pass

                    # hey, kiddo, how did that go?
                    max_tries = 10
                    tries     =  0
                    while tries < max_tries:
                        try:
                            wpid, wstat = os.waitpid(self.child, os.WNOHANG)

                        except OSError as e:

                            # this should not have failed -- child disappeared?
                            if e.errno == errno.ECHILD:
                                self.exit_code   = None
                                self.exit_signal = None
                                wstat            = None
                                break

                            # other errors are bad, but there is not much to
                            # be done at this point
                            raise

                        if wpid:
                            break

                        time.sleep(0.1)
                        tries += 1


            # at this point, we declare the process to be gone for good
            self.child = None

            # lets see if we can perform some post-mortem analysis
            if wstat is not None:

                if os.WIFEXITED(wstat):
                    # child died of natural causes - perform autopsy...
                    self.exit_code   = os.WEXITSTATUS(wstat)
                    self.exit_signal = None

                elif os.WIFSIGNALED(wstat):
                    # murder!! Child got killed by someone!  recover evidence...
                    self.exit_code   = None
                    self.exit_signal = os.WTERMSIG(wstat)

            try:
                if self.parent_out:
                    os.close(self.parent_out)
                    self.parent_out = None

            except OSError:
                pass

          # try:
          #     if self.parent_in:
          #         os.close(self.parent_in)
          #         self.parent_in = None
          # except OSError:
          #     pass

          # try:
          #     os.close(self.parent_err)
          # except OSError:
          #     pass


    # --------------------------------------------------------------------
    #
    def wait(self, timeout=None):
        '''
        blocks forever (or until timeout) until the child finishes on its own or
        is getting killed.
        '''

        with self.rlock:

            start = time.time()
            while True:

                if not self.alive():
                    return True

                if timeout and time.time() - start > timeout:
                    return False

                time.sleep(_POLLDELAY)


    # --------------------------------------------------------------------
    #
    def alive(self):
        '''
        determine if the child process is still active.  If not, mark
        the child as dead and close all IO descriptors etc (:func:`kill`).
        '''

        with self.rlock:

            # do we have a child which we can check?
            if not self.child:
                return False

            wstat = None
            while True:
              # print 'waitpid %s' % self.child

                # hey, kiddo, whats up?
                try:
                    wpid, wstat = os.waitpid(self.child, os.WNOHANG)

                except OSError as e:
                    if e.errno == errno.ECHILD:
                        # child disappeared, go to zombie cleanup routine
                        break

                    raise

                # did we get a note about child termination?
                if 0 == wpid:
                    # nope, all is well - carry on
                    return True

                # Yes, we got a note.
                # Well, maybe the child fooled us and is just playing dead?
                if os.WIFSTOPPED(wstat) or os.WIFCONTINUED(wstat):
                  # print 'waitpid %s : %s - %s -- stop/cont' \
                  #         % (self.child, wpid, wstat)
                    # we don't care if someone stopped/resumed the child --
                    # that is up to higher powers.  For our purposes, the
                    # child is alive.  Ha!
                    continue

                break

            # so its dead -- make sure it stays dead, to avoid zombie
            # apocalypse...
          # print "he's dead, honeybunny, jim is dead..."
            self.child = None
            self.kill(wstat=wstat)


    # --------------------------------------------------------------------
    #
    def returncode(self):

        with self.rlock:
            if not self.child:
                return self.exit_code


    # --------------------------------------------------------------------
    #
    def exit_signal(self):

        with self.rlock:
            if not self.child:
                return self.exit_signal


    # --------------------------------------------------------------------
    #
    def read(self, size=0, timeout=0, _force=False):
        '''
        read some data from the child.  By default, the method reads whatever is
        available on the next read, up to _CHUNKSIZE, but other read sizes can
        be specified.

        The method will return whatever data it has at timeout::

          timeout == 0: return the content of the first successful read, with
                        whatever data up to 'size' have been found.
          timeout <  0: return after first read attempt, even if no data have
                        been available.

        If no data are found, the method returns an empty string (not None).

        This method will not fill the cache, but will just read whatever data it
        needs (FIXME).

        Note: the returned lines do *not* get '\\\\r' stripped.
        '''

        with self.rlock:

            # start the timeout timer right now.  Note that even if timeout
            # is short, and child.poll is slow, we will nevertheless attempt
            # at least one read...
            start = time.time()
            ret   = ''

            # read until we have enough data, or hit timeout ceiling...
            while True:

                # first, lets see if we still have data in the cache we
                # can return
                if len(self.cache):

                    if not size:
                        ret        = self.cache
                        self.cache = ''
                        self.tail += ret
                        self.tail  = self.tail[-256:]
                        return ret

                    # we don't even need all of the cache
                    elif size <= len(self.cache):
                        ret        = self.cache[:size]
                        self.cache = self.cache[size:]
                        self.tail += ret
                        self.tail  = self.tail[-256:]
                        return ret

                # otherwise we need to read some more data, right?  idle
                # wait 'til the next data chunk arrives, or 'til _POLLDELAY
                rlist, _, _ = select.select([self.parent_out], [], [],
                                             _POLLDELAY)
                # got some data?
                for f in rlist:
                    # read whatever we still need

                    readsize = _CHUNKSIZE
                    if size:
                        readsize = size - len(ret)

                    buf = os.read(f, readsize)

                    if len(buf) == 0 and sys.platform == 'darwin':
                        self.kill()
                        raise RuntimeError('unexpected EOF: %s' % self.tail)

                    self.cache += buf.replace('\r', '')


                # lets see if we still got any data in the cache we
                # can return
                if len(self.cache):

                    if not size:
                        ret        = self.cache
                        self.cache = ''
                        self.tail += ret
                        self.tail  = self.tail[-256:]
                        return ret

                    # we don't even need all of the cache
                    elif size <= len(self.cache):
                        ret        = self.cache[:size]
                        self.cache = self.cache[size:]
                        self.tail += ret
                        self.tail  = self.tail[-256:]
                        return ret

                # at this point, we do not have sufficient data -- only
                # return on timeout

                if timeout == 0:
                    # only return if we have data
                    if len(self.cache):
                        ret        = self.cache
                        self.cache = ''
                        self.tail += ret
                        self.tail  = self.tail[-256:]
                        return ret

                elif timeout < 0:
                    # return of we have data or not
                    ret        = self.cache
                    self.cache = ''
                    self.tail += ret
                    self.tail  = self.tail[-256:]
                    return ret

                else:  # timeout > 0
                    # return if timeout is reached
                    now = time.time()
                    if now - start > timeout:
                        ret        = self.cache
                        self.cache = ''
                        self.tail += ret
                        self.tail  = self.tail[-256:]
                        return ret


    # ----------------------------------------------------------------
    #
    def write(self, data):
        '''
        This method will repeatedly attempt to push the given data into the
        child's stdin pipe, until it succeeds to write all data.
        '''

        with self.rlock:

            # attempt to write forever -- until we succeeed
            while data:

                # check if the pty pipe is ready for data
                _, wlist, _ = select.select([], [self.parent_in], [],
                                            _POLLDELAY)

                for f in wlist:

                    # write will report the number of written bytes
                    size = os.write(f, data)

                    # otherwise, truncate by written data, and try again
                    data = data[size:]


# ------------------------------------------------------------------------------

