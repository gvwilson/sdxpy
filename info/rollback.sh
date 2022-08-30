while [ true ];
do
    git log -n 1 --date=short --pretty=format:"%h %ad" >> ~/rollback.log
    wc -w $(find . -name '*.md') | fgrep total >> ~/rollback.log
    git reset --hard HEAD~1
    sleep 1
done
