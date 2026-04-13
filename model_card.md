# 🎧 Model Card: Music Recommender Simulation

## LookForSongsIlike2000DX 1.0

## 2. Intended Use  


The recommender recommends songs from a predefined list to the user based on their preference. 

---

## 3. How the Model Works  

The recommender takes the energy, the genre, the mood, danceability and acousticness into coinsideration when recommending songs.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- The catalog contains 22 songs.  
- Genres represented: pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop (8 genres total).  
- Moods represented: happy, chill, intense, relaxed, moody, focused (6 moods total).  
- Did you add or remove data  
- Several common taste dimensions are absent from the dataset: no classical, R&B, country, or metal genres; no "sad" or "angry" moods.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

The system best fits listeners that are loyal to their genre and energy consistent, essentially listeners who know exactly what they want. 
The recommender also offer little variety in its recommendation so don't expect it to give you varying results on different days.


---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

- conficting edgecases such as high tempo latin jazz or high energy sad power ballads can be confusing to the recommender.
- Genres is over prioritized which suppresses discovery across genre line.
- acoustic is binary and not a spectrum.
- the scoring favors dancability over calm or ambient.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

- further expand the genre relating table to allow more mixed genres.
- Better and more detailed recommendation explaination.  

---

## 9. Personal Reflection  

- What you learned about recommender systems  
- nothing about music is suppose to be binary, components are always in a spectrum and often a multi dimension one. The weight of some components also change in based on the value of another based on a persons taste. 
Basically the perfect recommender doesn't exist and all of them come with some compromise.
A good recommender however captures the aspects of a persons taste well and will be able to offer variety and exploration.