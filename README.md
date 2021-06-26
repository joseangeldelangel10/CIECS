# CIECS - *Car Info Entretainment and Control System*

**CIECS** this system was created as a project for a college course, the project consisted in 
designing a Car Info Entertainment System that should be able to reproduce mp3 songs stored in
an SD Card. The system should also be able to display in some way the details of each song, 
such as: name of each mp3 file, the name of the song, artists, album, release date, sampling 
rate and digitalization type. Another system requirement was that the system should give the 
user the possibility to pause the song, play the next song and play the previous song.

Once the project was completed we were able to display a GUI in the official RaspberryPI 7"
display using kivy framework. We were also able to reproduce mp3 files and to control car luxuries.

For further details please refer to the report found at:
https://drive.google.com/file/d/1roVKvkTU1Aj1GDYk1zVPgRM2NIGOw_m0/view?usp=sharing

Developed by: **Jose Angel Del Angel Dominguez and Leonardo Javier Nava Castellanos**


## Video Walkthrough

Here's a walkthrough of implemented user stories:

<img src= 'walkthrough.gif' title='Video Walkthrough' width='' alt='Video Walkthrough' />


Here's a walkthrough of landscape functionality:

<img src= 'walkthrough2.gif' title='Video Walkthrough' width='' alt='Video Walkthrough' />

GIF created with [LiceCap](https://www.cockos.com/licecap/).

## Challenges when developing the app

**Getting youtube video url and passing it through diferent classes:**

Youtube video feature was a whole challenge that involved getting the id of a certain movie, using such id to get the video url and generating the Youtube player view. 

In this challenge the time at wich the youtube url was retrived was crucial, since we should already have the youtubr url before generating the youtube player view and thus, url culdn't be retrivered in the MovieTrailer activity. To solve this we retrived the URL in the MovieDescription activity wrapping it and passing it to the MovieTrailer activity.

**Modern android versions avoiding icons in toolbar**

Modern versions of android made difficult to have an icon displayed inside of the toolbar, and since many android forums are out of date with that feature a large research was done. 

**Retriving reviews and wrapping two arguments**

In order to get the movie reviews we implemented a process similar to the one found in Youtube Player View; nontheless creating our own recycled view, the required adapter and all the methods required for such recycled view was a challenge and a huge opportunity to lear about Recycled Views. To make the youtube videos task easier the View Holders in the recycled view contain text views instead of complex views.

Since we should used the movie id to get reviews that would be displayed in the same window as the yt video, we wrappped and passed to the MovieTrailer the youtube video URL and the movie id (two different items) using a string array containing both elements (movie id and youtube URL).

