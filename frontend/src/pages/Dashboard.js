import "./Dashboard.css";
import wizkid from "../assets/wizkid.jpg";

export default function Dashboard() {
  return(
    <div className="dashboardBody">
      <header>
        <h1>tuneshift</h1>
        {/* replace with users spotify image */}
        <button style={{'display':'none'}}>logout</button>
        <img src={wizkid} alt="holder"/>
      </header>
      <div>
        <h2>Add Song</h2>
        <input></input>
        <button>Song Name</button>
      </div>
      <div>
        <div>
          <p>Name</p>
          <p>Album</p>
          <p>Release Date</p>
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
