# marathon-pace-recommender

## Live Website

https://pace-recommender.herokuapp.com

https://user-images.githubusercontent.com/64169932/188011902-6457ca55-a8e4-43a6-a6ae-07947f57aeaf.mov

As a new runner 🏃 training for his first marathon, one of the things I'm struggling with is coming up with a proper pacing strategy for race day. 

And then it hit me 💡... why don't I learn from runners who have already ran their first marathon? So, I looked at historical data on the world-famous Berlin marathon and examined the pacing strategy of runners who have experienced significant improvements on their finish time (e.g. > 30 mins).

I then used a neural network to learn from this data and determine the best pacing strategy for a projected finish time. Moreover, the user has the option to change the outputted pacing strategy using elevation data!

## Reproducing Steps (Mac OS)
1. Run `git clone https://github.com/samliu21/marathon-pace-recommender`. This will download a folder called `marathon-pace-recommender` containing all of the necessary files.
2. Navigate into the folder using `cd marathon-pace-recommender`.
3. Create a virtual environment using `python -m venv .` and activate it with `source bin/activate`.
4. Install the necessary dependencies using `python -m pip install -r requirements.txt`.

## Data
The following <a href="https://github.com/AndrewMillerOnline/marathon-results/tree/main/Berlin">dataset</a> was used. Here is the data cleaning process:

- Use `manipulate_data.py` to clean the data into a usable format
- Use `get_race_data.py` to get the novel races

### Manipulating the data
To use `manipulate_data.py`, we call `python manipulate_data.py [data_file_to_manipulate] [options]` (e.g. `python manipulate_data.py ../data/berlin-2015.csv -o -s`).

- `-duc` or `--dropcol` drops unnecessary columns in the table
- `dn` or `--dropnull` drops rows that contain null values
- `-o` or `--sort` sorts the data file by name and nationality
- `-u` or `--unique` drops rows that cannot be uniquely represented by name and nationality
- `-s` or `--save` saves the changed csv file
- `-a` or `--all` calls all of the above

For more information, look at the `data_cleaning` folder.

## Model
The model is a simple neural network made of dense layers.

```
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 dense (Dense)               (None, 1)                 2         
                                                                 
 dense_1 (Dense)             (None, 16)                32        
                                                                 
 dense_2 (Dense)             (None, 32)                544       
                                                                 
 dense_3 (Dense)             (None, 10)                330       
                                                                 
=================================================================
Total params: 908
Trainable params: 908
Non-trainable params: 0
_________________________________________________________________
```
