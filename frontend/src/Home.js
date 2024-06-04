import "./Home.css";

export default function Home() {
  return (
    <div className="home-body">
      <header>
        <h1>tuneshift</h1>
        <button className="top-login">login with spotify</button>
      </header>
      <div className="home-main">
        <div className="main-text">
          <p>
            Want to move your songs from apple music to spotify? or copy a
            playlist from apple music to spofity now with tuneshift just login
            to spofity and enter the link to the public apple playlist and copy
            the songs. Also make a playlist with the billboard hot 100 from a
            particular date just enter the date and get a spotify playlist with
            the songs.
          </p>
          <button>Get started with Spotify</button>
        </div>
        <div className="main-img"></div>
      </div>
      <footer>
        <p>&copy <a href="">andrew a.</a></p>
        <img src="#" alt="github"/>
      </footer>
    </div>
  );
}
