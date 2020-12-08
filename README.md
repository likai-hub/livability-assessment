With rapid urbanization, retrieving livability information of human settlements in time is essential for urban planning and governance. However, livability assessment is often limited by data availability and their update cycle, and this problem is more serious when making assessment at finer spatial scales (e.g., community level). We develop a reliable and dynamic model for community-level livability assessment, which provides detailed and useful information of human settlements for sustainable urban planning and governance. Here we present the code for the main procedures of data processing described in the Methods section in our manuscript (Zhu et al., 2020. Remote Sensing, Under Review).

1 fit_weights_calculating_livability_score_montecarlo.R 
    R script (1) to fit the AHP-derived weights for each index with probability functions including exponential, normal, gamma, and so forth, and (2) to calculate livability score and its uncertainty of each community with combined weighted-sum method and Monte Carlo simulations.
2 Run_ahp_all_questionaire.py
    Python script to carry out the AHP analysis to derive the weight for each index for all collected questionnaires. The AHP function will be cited when running this script, which is also uploaded (see file, ahpy.py)
3 Gapfilling-daily-modLST.py
    Python script to gapfill the cloud-contaminated pixels within MODIS daily land surface temperature products. The code is written based on the hybrid method developed by Li et al. (2017). 
4 POI-retrievals-BAIDU-API.py
    Python script to retrieve POIs of specific types (e.g., shops and restaurants) from the Baidu Map API. 
5 Travel-distance-calculation-BAIDU-API.py 
    Python script to retrieve the travel (e.g., driving, biking or walking) distance between two places from the Baidu Map API. 
6 walking_distance_to_nearest_parks_baidu_map.py
    Python script to retrieve the walking distance to the nearest park from the Baidu Map API. 
7 Retrieve-trafic-status-grids-of-fishnet-BAIDU-API.py
    Python script to retrieve the frequency of traffic jam within predefined fishnet and specific time period from the Baidu Map API.
8 Retrieval-login-count-grids-Tencent-API.py
    Python script to retrieve the times of social media (QQ chat software) login from the Tencent API.
9 Retrieve-housing-prices-communites-Lianjia.py
    Python script to retrieve the average trade prices of second-hand houses for communities in our study area.
   
