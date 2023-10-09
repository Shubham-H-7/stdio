import pysftp


def testSftpConnection(sftp_host, sftp_port, sftp_username, sftp_password, private_key_path):
    if not private_key_path:
        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            with pysftp.Connection(host=sftp_host, port=sftp_port, username=sftp_username, password=sftp_password,
                                   cnopts=cnopts):
                return "SFTP Connection Successful"
        except Exception as e:
            return f"SFTP Connection Failed: {str(e)}"
    else:
        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None

            with pysftp.Connection(host=sftp_host, port=sftp_port, username=sftp_username, private_key=private_key_path,
                                   cnopts=cnopts):
                return "SFTP Connection Successful"
        except Exception as e:
            return f"SFTP Connection Failed: {str(e)}"
