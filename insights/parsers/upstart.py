"""
UPstart - Command ``initctl --system list``
===========================================

Parser to parser the output of ``initctl --system list`` commands.
"""

from insights import parser, CommandParser
from insights.parsers import SkipException
from insights.specs import Specs


@parser(Specs.initctl_lst)
class UPstart(CommandParser):
    """
    Class to parse the output of initctl command. It allows a
    system administrator to communicate and interact with the
    Upstart init(8) daemon and list the services managed by
    Upstart init.

    Sample output::

        rc stop/waiting
        vmware-tools start/running
        tty (/dev/tty3) start/running, process 9499
        tty (/dev/tty2) start/running, process 9495
        tty (/dev/tty1) start/running, process 9493
        tty (/dev/tty6) start/running, process 9507
        tty (/dev/tty5) start/running, process 9505
        tty (/dev/tty4) start/running, process 9502
        tty (/dev/ttyS0) start/running, process 9509
        plymouth-shutdown stop/waiting
        control-alt-delete stop/waiting
        rcS-emergency stop/waiting
        readahead-collector stop/waiting
        kexec-disable stop/waiting
        quit-plymouth stop/waiting
        rcS stop/waiting
        prefdm stop/waiting
        init-system-dbus stop/waiting
        ck-log-system-restart stop/waiting
        readahead stop/waiting
        ck-log-system-start stop/waiting
        splash-manager stop/waiting
        start-ttys stop/waiting
        readahead-disable-services stop/waiting
        ck-log-system-stop stop/waiting
        rcS-sulogin stop/waiting
        serial stop/waiting

    Raises:
        SkipException: When nothing need to parse.

    Attributes:
        upstart_managed: This returns daemon details.
        daemon_status: This returns daemon status.
        dev_status: This returns device status.


    Examples:
        >>> type(upstart_obj)
        <class 'insights.parsers.upstart.UPstart'>
        >>> upstart_obj.upstart_managed('vmware-tools')
        'vmware-tools start/running'
        >>> upstart_obj.daemon_status('vmware-tools')
        'start/running'
        >>> upstart_obj.daemon_status('start-ttys')
        'stop/waiting'
        >>> upstart_obj.dev_status('/dev/tty4')
        'stop/waiting'
        >>> upstart_obj.upstart_managed('/dev/tty3')
        'tty (/dev/tty3) start/running, process 9499'
    """

    def parse_content(self, content):
        self.data = []
        self.tty = {}
        self.daemon_proc = {}
        if (not content):
            raise SkipException("No Contents")
        for line in content:
            self.data.append(line)
            if 'dev/tty' in line:
                line_s = line.split()
                if len(line_s) > 1:
                    dev = line_s[1].replace('(', '').replace(')', '')
                    self.tty[dev] = {}
                    self.tty[dev]['status'] = line_s[2].replace(',', '')
                    if len(line_s) > 4 and 'process' in line:
                        self.tty[dev]['process'] = str(line_s[4])
            else:
                line_s = line.split()
                proc = line_s[0]
                status = line_s[1]
                self.daemon_proc[proc] = status

    def upstart_managed(self, daemon):
        """
        (str): This method returns the status of daemon service if it is managed by upstar else it will return `None`.
        """
        for line in self.data:
            if daemon in line:
                return line
        return None

    def daemon_status(self, daemon):
        """
        (str): This method will return the status of the process `start/running` or `stop/waiting` if it is managed by upstart else it will return `None`.
        """
        return self.daemon_proc.get(daemon, None)

    def dev_status(self, dev):
        """
        (str): This method will return the status of the tty device `start/running` or `stop/waiting`, along with `process-ID`i if it is managed by upstart else it will return `None`.
        """
        if dev and dev in self.tty.keys():
            return self.tty[dev].get('status', None)
