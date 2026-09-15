@echo off
echo =======================================================
echo  Updating Amazon Affiliate Store on GitHub (user: KNicP)
echo  Telegram Channel: @amazonoffershub1
echo =======================================================

cd /d d:\aff

git add .
git commit -m "Configured Telegram Bot token and channel @amazonoffershub1"
git push origin main

echo =======================================================
echo  SUCCESS! Updated configuration pushed to GitHub:
echo  https://github.com/KNicP/amazon-affiliate-store
echo =======================================================
pause
