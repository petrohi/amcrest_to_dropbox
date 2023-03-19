# Automatic upload of Amcrest media to Dropbox

## Setup

### 1. Install Python and FFMPEG
```
sudo apt update
sudo apt upgrade
sudo apt install python3-pip ffmpeg
```
### 2. Setup `sftp` group, `sftp_amcrest` user, its password, and configure `sshd` server
```
sudo mkdir /var/lib/sftp
sudo groupadd sftp
sudo useradd --base-dir /var/lib/sftp --create-home -g sftp sftp_amcrest
sudo passwd sftp_amcrest
sudo bash -c 'cat <<EOF >> /etc/ssh/sshd_config
Match group sftp
ChrootDirectory /var/lib/sftp
X11Forwarding no
AllowTcpForwarding no
ForceCommand internal-sftp
EOF'
sudo systemctl restart ssh
```
### 3. Setup camera
3.1 Set camera video settings to H.265 and 720P
![camera_video](/doc/camera_video.png)
3.2 Set desired recording schedule
![storage_record_schedule](/doc/storage_record_schedule.png)
3.3 Set storage recording destination path to FTP
![storage_record_destination](/doc/storage_record_destination.png)
3.4 Set SFTP settings
![storage_record_destination_ftp](/doc/storage_record_destination_ftp.png)
3.5 Take note of camera serial number (S/N)
![information_version](/doc/information_version.png)
### 4. Create Dropbox app
4.1 Create new Dropbox App
![dbx_create_app](/doc/dbx_create_app.png)
4.2 Set App permissions for `files.content.write`
![dbx_set_app_permissions](/doc/dbx_set_app_permissions.png)
4.3 Take note of App key 
![dbx_app_key](/doc/dbx_app_key.png)
### 5. Setup sync cron job
5.1 Login as `sftp_amcrest`
```
sudo -u sftp_amcrest bash
cd
```
5.2 Install latest `amcrest_to_dropbox` release
```
export TAG=0.0.2
wget https://github.com/petrohi/amcrest_to_dropbox/archive/refs/tags/${TAG}.tar.gz
tar xf ${TAG}.tar.gz
mv amcrest_to_dropbox-${TAG}/*.py .
mv amcrest_to_dropbox-${TAG}/*.toml .
mv amcrest_to_dropbox-${TAG}/*.txt .
rm -r ${TAG}.tar.gz amcrest_to_dropbox-${TAG}/
pip install -r requirements.txt
```
5.3 Authenticate with Dropbox. This command will print Dropbox user email and refresh token.
```
DROPBOX_APP_KEY=<YOU APP KEY> ./auth_dropbox.py
```
5.4 Edit `refresh_token` and camera(s) `serial` in `sync_dropbox.toml`
```
nano sync_dropbox.toml
```
5.5 Test sync with Dropbox
```
DROPBOX_APP_KEY=<YOU APP KEY> /var/lib/sftp/sftp_amcrest/sync_dropbox.py /var/lib/sftp/sftp_amcrest/sync_dropbox.toml
```

5.6 Setup cron job
```
crontab -e
```
Paste folowing line at the end of edited file
```
15 * * * * DROPBOX_APP_KEY=<YOU APP KEY> /var/lib/sftp/sftp_amcrest/sync_dropbox.py /var/lib/sftp/sftp_amcrest/sync_dropbox.toml >> /var/lib/sftp/sftp_amcrest/sync_dropbox.log
```