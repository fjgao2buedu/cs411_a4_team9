const BASE_API_URL = "https://";
const URL_EXTENSION_= "/"
export const GET_URL = (_: string) => {return _}

export const TOKEN = process.env.REACT_APP_||"";

export const GET_DEFAULT_HEADERS = () => {
  var headers = new Headers();
  headers.append('accept', 'application/json')
  headers.append('x-functions-key', TOKEN)
  return headers;
};


