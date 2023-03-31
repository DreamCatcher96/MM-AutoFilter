if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/jikkubot32/DQ-Join.git /DQ-Join
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /DQ-Join
fi
cd /DQ-Join
pip3 install -U -r requirements.txt
echo "Starting DQ-Join...."
python3 bot.py
