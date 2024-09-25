import "./Dashboard.css";
import wizkid from "../assets/wizkid.jpg";
import arrow from "../assets/down-arrow.png";
import { useState } from "react";

export default function Dashboard() {
  const [showLog, setShowLog] = useState(false);
  const [showMenu, setShowMenu] = useState(false);
  const [method, setMethod] = useState("name");

  function addSong(){}
  function billboard(){}
  function applePlaylist(){}

  return(
    <div className="dashboardBody">
      <header>
        <h1>tuneshift</h1>
        {/* replace with users spotify image */}
        <div className="headerHolder">
          {showLog && <button>logout</button>}
          <img className="headerImg" onClick={() => setShowLog(!showLog)} src={wizkid} alt="holder"/>
        </div>
      </header>
      <div className="addContainer">
        <h2>Add Song(s)</h2>
        <input placeholder="Enter song name" className="songInput"/>
        {/* make the values of the select proper */}
        <select value={"blah"}>
          <option value="song">Song Name</option>
          <option value="billboard">Add Billboard hot 100</option>
          <option value="apple">Add Apple Playlist</option>
        </select>
      </div>
      <div>
        <div>
          <p>Name</p>
          <p>Album</p>
          <p>Release Date</p>
          <p>Genre</p>
          <p>Time</p>
        </div>
        {/* create display for if there are no songs that says there are no songs added yet or something */}
        <div className="songs">
          <div className="songCard">
            <img src={wizkid}/>
            <div>
              <p>Essense</p>
              <p>Wizkid, Tems</p>
            </div>
            <p>Made in Lagos</p>
            <p>January 1st, 2021</p>
          </div>
          <div className="songCard">
            <img src={wizkid}/>
            <div>
              <p>Essense</p>
              <p>Wizkid, Tems</p>
            </div>
            <p>Made in Lagos</p>
            <p>January 1st, 2021</p>
          </div>
          <div className="songCard">
            <img src={wizkid}/>
            <div>
              <p>Essense</p>
              <p>Wizkid, Tems</p>
            </div>
            <p>Made in Lagos</p>
            <p>January 1st, 2021</p>
          </div>
          <div className="songCard">
            <img src={wizkid}/>
            <div>
              <p>Essense</p>
              <p>Wizkid, Tems</p>
            </div>
            <p>Made in Lagos</p>
            <p>January 1st, 2021</p>
          </div>
          <div className="songCard">
            <img src={wizkid}/>
            <div>
              <p>Essense</p>
              <p>Wizkid, Tems</p>
            </div>
            <p>Made in Lagos</p>
            <p>January 1st, 2021</p>
          </div>
        </div>
        <div>
          <button>help</button>
          <button>Create Playlist</button>
        </div>
      </div>
    </div>
  )
}
