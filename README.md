# Driver-Search

This is a repository for a web app designed using streamlit to help Drosophila neuroscientists identify Gal4 driver lines.

I initially tried to host the app using streamlit cloud, but the underlying data is too large to host the app on their free cloud service. Instead of accessing the web 
app publicly, users can download the source code/data here and run the app on their local computer by following these instructions.

To use this app on your local machine, you will need to have python

## Instructions to access the app

1) Clone this repo to your local machine
2) Open the driver-search-app.py file in vscode and run it
    - note that this app depends on streamlit, numpy, pandas, and plotly. You will need to have these packages 
      installed in order for the app to work!
3) You will get a warining message in the vscode terminal like this: 

        "Warning: to view this Streamlit app on a browser, run it with the following command: streamlit run **pathname**"

    Copy `streamlit run` and the pathname after it, paste that code into the terminal, and run it. 

After following these three steps, the web app should open in a web browser and you can then use it!
    
