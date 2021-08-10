# Contributing to the documentation

The documentation is written in markdown and then generated with [mkdocs](https://www.mkdocs.org/).
Required libraries are installed if you've followed the [development environment documentation](../dev/dev-env.md) of the project.

Graphs and diagrams are generated by the [Mermaid library](https://mermaid-js.github.io/mermaid/#/).

Update the documentation in the `docs` folder placed in the root of the project.

Run dev server locally to check the result
```bash
mkdocs serve -a 0.0.0.0:4000
```

The page is available on [http://127.0.0.1:4000](http://127.0.0.1:4000).

Send a pull request then to propose your changes to the project.

## Notes

### Reset your gh-pages branch to match the upstream

If you've built mkdocs and published a version in your fork for testing, your `gh-pages` branch will differ from the 
upstream repository. 

To reset your local `gh-pages`, follow the procedure below:
```bash
# delete local branch
git branch -D gh-pages
# delete remote branch (fork here is your remote. Replace by origin if needed)
git push -d fork gh-pages
# checkout gh-pages
git checkout --orphan gh-pages
# pull last version (upstream is the remote name of the main repo)
git pull upstream gh-pages
# (optional) force push to your fork to override changes
git push -f fork gh-pages
# go back to your original branch
git checkout master
```