import axios from "axios";

//const baseDomain = "https://sogor98.eu.pythonanywhere.com/";
const baseDomain = "http://localhost:3333";
const baseURL = `${baseDomain}`; // Incase of /api/v1;
axios.defaults.withCredentials = true

// ALL DEFUALT CONFIGURATION HERE

export default axios.create({
  baseURL,
  credentials: 'include',

  headers: {
    credentials: 'include',
    withCredentials: "include"
    // "Authorization": "Bearer xxxxx"
  }
});
