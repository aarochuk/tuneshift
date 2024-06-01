import './Home.css';

export default function Home() {
  return (
    <>
    <div className='tester'>

    </div>
    <div className="home-root">
      <header>
        <h1>jamshift</h1>
        <button>Login with spotify</button>
      </header>
      <div className="main">
        <div className="main-text">
          Want to copy a public playlist from apple to spotify? With jamshift
          just copy the link to the playlist and make a new spotify playlist
          with the songs. Also you can now make a playlist with the billboard
          hot100 from a particular date just input the date and get a playlist
          on spotify with the songs from that date.
          <button>Login with spotify</button>
        </div>
      </div>
      <footer>
        <p>&copy andrew a. 2024</p>
        <p>Github</p>
      </footer>
    </div>
    </>
  );
}
