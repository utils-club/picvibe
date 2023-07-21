export const fetch_data = async function (api_url) {
    try {
      const response = await fetch(api_url);
      const data = await response.json();
      return data;
    } catch (error) {
      console.log("Error fetching data: ", error);
    }
  }