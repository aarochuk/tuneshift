import "./Home.css";
import wizkid from "../assets/wizkid.jpg";
import spotify from "../assets/spotify.png";
import gh from "../assets/github.png";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Home() {
  let navigate = useNavigate();

  const loginSpotify = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/spotifyAuth");
      console.log(response.data)
      if (response.data.state == 1){
        navigate("/dashboard")
      }
    } catch (error) {
      console.log("Error Occured");
    }
  };

  return (
    <div className="home-body">
      <header>
        <h1>tuneshift</h1>
      </header>
      <div className="home-main">
        <div className="main-text">
          <h2>wanna move songs from apple music to spotify?</h2>
          <p>
            With tuneshift just login to spofity and enter the link to the
            public apple playlist and copy the songs to a spotify playlist. Also
            make a playlist with the billboard hot 100 from a particular date
            just enter the date and get a spotify playlist with the songs.
          </p>
          <button className="top-login" onClick={loginSpotify}>
            <img src={spotify} alt="" />
            Get started with Spotify
          </button>
        </div>
        <div className="main-img">
          <div className="img-holder">
            <div className="wiz">
              <img className="wizzy-boi" src={wizkid} alt="wizkid" />
            </div>
            <p className="genre">August 2020 &#x2022; Afrobeat</p>
            <p className="sname">Essense</p>
            <p className="sartist">Wizkid</p>
          </div>
        </div>
      </div>
      <footer>
        <p>
          &copy;{" "}
          <a
            href="https://www.linkedin.com/in/acarochu/"
            target="_blank"
            rel="noreferrer"
          >
            andrew a.
          </a>
          {"   "}
          2024
        </p>
        <a href="https://github.com/aarochuk" target="_blank" rel="noreferrer">
          <img src={gh} alt="github" />
        </a>
      </footer>
    </div>
  );
}
