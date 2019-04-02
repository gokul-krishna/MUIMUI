# Work Plan
For now we will track our work plan in `README.md`

we will use `nbs` folder for testing the ideas or frameworks in Jupyter notebooks.  
only tested code would be moved to `src`

## Tasks
- [x] Make list of Instagram (ig) influencers 
- [x] Make list of Websites to scrape
- [x] Prioritize the type of wardrobe we are going to focus on `V0`
- [x] Decide on ig scraping mechanism
- [x] Make template for website scraping
- [ ] Get a working version of auto-encoder notebook for the open fashion dataset
- [ ] Make wireframes for front-end
- [ ] get `v0` pipeline for backend
... add all the task here

# Environment Setup
We will be using a ubuntu image for hosting server to make things simple.
Run the [setup script](setup.sh) to set up the *muimui* environment and install required dependencies.

To make *muimui* conda environment available in jupyter run the following commands:
```bash
pip install ipykernel
python -m ipykernel install --user --name muimui --display-name "muimui"
```

We are using this [Instagram scraper](https://github.com/rarcega/instagram-scraper)
