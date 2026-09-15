@echo off
echo =======================================================
echo  Updating Amazon Affiliate Store on GitHub (user: KNicP)
echo  Posting Frequency: Every 2 minutes (Local) / 5 mins (Cloud)
echo =======================================================

cd /d d:\aff

git add .
git commit -m "Updated deal posting frequency to every 2 minutes"
git push origin main

echo =======================================================
echo  SUCCESS! Changes pushed to GitHub:
echo  https://github.com/KNicP/amazon-affiliate-store
echo =======================================================
pause
