import "./Dashboard.css";
import wizkid from "../assets/wizkid.jpg";
import question from "../assets/question.png";
import search from "../assets/search.png";
import { useLocation } from "react-router-dom";
import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  let navigate = useNavigate();
  const {state} = useLocation();
  const [showLog, setShowLog] = useState(false);
  const [method, setMethod] = useState("song");
  const [songList, addSongList] = useState([]);
  const [searchVal, setSearchVal] = useState("");
  const [plName, setPlName] = useState("");
  const [isHovered, setIsHovered] = useState(false);

  function methodChange(e) {
    setMethod(e.target.value);
  }

  // add error handling and make sure searches are not done unless the searchVal is actually set to something

  function deleteClicked(index){
    const temp = [...songList]
    temp.splice(index, 1)
    addSongList(temp)
  }

  function findSong(){
    if(method==="song"){
      addSong()
    }else if(method==="billboard"){
      billboard()
    }else{
      applePlaylist()
    }
  }

  const createPlaylist = async () =>{
    if(plName.length > 0){
      try {
        const response = await axios.post("http://127.0.0.1:8080/createPlaylist", {songs: songList, playlist_name:plName});
        console.log(response.data);
        addSongList([])
      } catch (error) {
        console.log("Error Occured");
      }
      setPlName("");
    }
  }

  const addSong = async () => {
    console.log(searchVal);
    try {
      const response = await axios.post("http://127.0.0.1:8080/addSong", {song: searchVal, id:songList.length});
      console.log(response.data);
      addSongList([response.data, ...songList])
      console.log(songList)
    } catch (error) {
      console.log("Error Occured");
    }
    setSearchVal("");
  };

  const billboard = async () => {
    console.log(searchVal)
    try {
      const response = await axios.post("http://127.0.0.1:8080/addBillboard", {date: searchVal, id:songList.length});
      console.log(response.data);
      addSongList([...response.data, ...songList])
      console.log(songList)
    } catch (error) {
      console.log("Error Occured");
    }
    setSearchVal("");
  };

  const applePlaylist = async () => {
    console.log(searchVal)
    try {
      const response = await axios.post("http://127.0.0.1:8080/addApplePlaylist", {playlist: searchVal, id:songList.length});
      console.log(response.data);
      addSongList([...response.data, ...songList])
      console.log(songList)
    } catch (error) {
      console.log("Error Occured");
    }
    setSearchVal("");
  };

  //console.log(state)
  return(
    <div className="dashboardBody">
      <header>
        <h1>tuneshift</h1>
        {/* replace with users spotify image */}
        <div className="headerHolder">
          {showLog && <button onClick={()=>navigate('/')}>logout</button>}
          <img className="headerImg" onClick={() => setShowLog(!showLog)} src={state.images[1].url} alt="holder"/>
        </div>
      </header>
      <div className="addContainer">
        <h2>Add Song(s)</h2>
        <div className="inputBox">
          {method==="song" && <input placeholder="Enter song name" value={searchVal} onChange={e=>setSearchVal(e.target.value)}/>}
          {method==="billboard" && <input placeholder="Enter date for hot 100 in format YYYY-DD-MM" value={searchVal} onChange={e=>setSearchVal(e.target.value)}/>}
          {method==="apple" && <input placeholder="Enter link to apple playlist" value={searchVal} onChange={e=>setSearchVal(e.target.value)}/>}
          <img src={search} onClick={findSong}/>
        </div>
        
        {/* make the values of the select proper */}
        <select value={method} onChange={methodChange}>
          <option value="song">Song Name</option>
          <option value="billboard">Add Billboard hot 100</option>
          <option value="apple">Add Apple Playlist</option>
        </select>
      </div>
      {/* if there are multiple songs with the same name from the songs the user wants to add make screen for them to select the right one */}
      {/**dont add multiple of the same song to the list */}
      {/**save songs from the last session to an aws database or firebase */}
      {/**add x to songs to remove songs from list */}
      {songList.length > 0 && <div className="songsHolder">
        <div className="songsHeader">
          <div className="songNameHolder">
            <p>Name</p>
          </div>
          <div className="otherSongDetails">
            <p>Time</p>
            <p>Album</p>
            <p>Link</p>
          </div>
        </div>
        <div className="songs">
          {songList.map((song, index)=>{
            return(
            <div className="songCard" key={song.id}>
            <div className="songNameHolder">
              <img src={song.img} onClick={()=>deleteClicked(index)}
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
                className={`${isHovered ? 'image-hovered' : ''}`}
              />
              <div>
                <p>{song.title}</p>
                <p>{song.artists.map((artist)=><span>{artist}{"   "}</span> )}</p>
              </div>
            </div>
            <div className="otherSongDetails">
              <p>{song.time}</p>
              <p>{song.album}</p>
              {/**fix styling of the link */}
              <p><a href={song.link} target="_blank">{song.title}</a></p>
            </div>
          </div>)
          })}
        </div>
        <div className="bottomButtons">
          {/* add functionality where when you click these buttons new screen would come on top of the screen, the screen darkens and you can use the functionality of these buttons */}
          <input type="text"  placeholder="New Playlist Name" value={plName} onChange={e=>setPlName(e.target.value)}/>
          <button className="createButton" onClick={createPlaylist}>Create Playlist</button>
          
        </div>
      </div>}
      
      {songList.length === 0 &&
      <div className="noSongs">
        <h2>Add to create playlist</h2>  
      </div>}
    </div>
  )
}
