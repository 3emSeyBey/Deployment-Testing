cd /root/Deployment-Testing
git pull origin main
source /root/Deployment-Testing/.venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart uvicorn
