# c2c-search
AI search agent for camptocamp.org

# CLI usage
```commandline
python chat-cli.py
```
sample interaction
```
Describe the mountain adventure are you looking for
>>> ski tour in mont-blanc range
Great! It sounds like you're interested in a ski touring outing in the Mont-Blanc range. Can you please provide me with the following information:
- The desired duration of the outing, in days.
- The minimum and maximum levels of difficulty you're looking for.
- The minimum and maximum amount of ascent you'd like to have, in meters.
>>> 1 or 2 days, PD to AD, at most 2000m of ascent
Great! It sounds like you're interested in a ski touring outing in the Mont-Blanc range. 
Based on your description, I have inferred the following details:
- Activity: Ski Touring
- Outing Area: Mont-Blanc range
- Duration: 1 or 2 days
- Difficulty: PD to AD
- Ascent: At most 2000m

Is my inference correct?
>>> yes
Great! Based on your description, it seems like you are looking for a ski touring outing in the Mont-Blanc range. Here are the details I have inferred:
- Activity: Ski Touring
- Geographical location: Mont-Blanc range
- Minimum duration: 1 day
- Maximum duration: 2 days
- Minimum difficulty: PD (not difficult)
- Maximum difficulty: AD (quite difficult)
- Minimum ascent: 0 meters
- Maximum ascent: 2000 meters

Please confirm if these details are correct.
>>> make the minimum ascent 1000m
Great! Based on the information you provided, here are the details of your desired mountain outing:

- Activity: Ski touring
- Area: Mont Blanc range
- Minimum duration: 1 day
- Maximum duration: 2 days
- Minimum difficulty: PD (not difficult)
- Maximum difficulty: AD (quite difficult)
- Minimum ascent: 1000 meters
- Maximum ascent: 2000 meters

Please confirm if these details are correct.
>>> this is correct
Great! Based on the information you provided, I have inferred the following details about your desired ski tour in the Mont-Blanc range:

- Activity: Skitouring
- Outing Area: Mont-Blanc range
- Minimum Duration: 1 day
- Maximum Duration: 2 days
- Minimum Difficulty: PD (not difficult)
- Maximum Difficulty: AD (quite difficult)
- Minimum Ascent: 1000m
- Maximum Ascent: 2000m

Please confirm if these details are correct.
>>> yes the details are correct
https://www.camptocamp.org/routes?bbox=754230.5681939817%2C5743547.737281935%2C774230.5681939817%2C5763547.737281935&act=skitouring&time=1%2C2&hdif=1000%2C2000&lrat=PD-%2CPD%2B
Thank you for providing the URL! Please click on the following link to navigate to the website and see the outings matching your search criteria: 

[Camptocamp Outings](https://www.camptocamp.org/routes?bbox=754230.5681939817%2C5743547.737281935%2C774230.5681939817%2C5763547.737281935&act=skitouring&time=1%2C2&hdif=1000%2C2000&lrat=PD-%2CPD%2B)

I wish you a fruitful search and hope you find the perfect outings for your skitouring adventure. Have a safe and enjoyable outing!

```
