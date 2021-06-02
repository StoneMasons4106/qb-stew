# QB Stew

QB Stew is an attempt to measure quarterback play as a whole, rather than pointing to one data point above the rest for an out of context narrative.

The metric was developed by [Bruce Nolan](https://mobile.twitter.com/BruceExclusive) of the [Bruce Exclusive on Buffalo Rumblings](https://open.spotify.com/show/5RYDNBKPj6d2zwdf3tmdmy), and it measures 7 things:

1. Passer Rating
2. QBR
3. ANY/A (Average Net Yards per Attempt)
4. Pro Football Focus Grade
5. DVOA
6. CPOE (Completion percentage over Expected)
7. EPA (Expected Points Added)

After these stats are gathered for the quarterbacks to be analyzed, they are then ranked based on how they measured. Their composite rank (add the 7 ranks, and divide by 7), becomes known as their 'QB Stew'.

Please note: For right now, only data for 2020 is available. I will continue to update data in the coming years for historical data, but this is what's available now. Additionally, only quarterbacks listed on [ESPN's QBR Rankings](https://www.espn.com/nfl/qbr) are available to be analyzed.

## Deployment

1. Ensure you have a fairly recent install of Python on your computer. (This program was developed in 3.8.10)
    * If you do not, you can visit these sites to find one... [Python.org](https://www.python.org/downloads/) or [Anaconda.org](https://www.anaconda.com/products/individual)
2. Once installed, clone the repository to your local directory, or simply copy the contents of the 'qb_stew.py' and 'requirements.txt' file into your local directory.
3. Find the directory with pip installed, and ensure the 'requirements.txt' file is there as well before you run 'pip install -r requirements.txt'.
    * If this does not work, run 'pip install pymongo' and 'pip install dnspython'.
        * All other libraries and dependencies can be found in the 'requirements.txt' file, and you can confirm that you have them by running 'pip show insert_module_name_here'.
4. After that, you should be able to run 'python qb_stew.py'.
    * Again, this will only work for 2020 right now. More data to come in the coming years.

## Issues

If you notice any issues, please kindly put them in the issue tracker. Thank you.