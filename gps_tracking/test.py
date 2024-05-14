import pickle
from FootballField import FootballField
f = open('sample_filled_field_slu.pkl','rb')
slu_field = pickle.load(f)

def timestamp_to_seconds(x):
    mins,seconds=x.split(':')
    mins=int(mins)
    seconds=int(seconds)
    if x[0]=='-':
        return mins*60-seconds
    else:
        return mins*60+seconds

secs=slu_field.coordinate_frame['Minute:Second'].apply(lambda x: timestamp_to_seconds(x))
print(secs.max())