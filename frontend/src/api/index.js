// API module for fetching data from the backend
const API_BASE_URL = "http://localhost:5000";

export const fetchCharacters = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/characters`);
    const data = await response.json();

    if (data.mode === "local" && data.characters) {
      // Transform the data to match the expected format
      return data.characters.map((char) => ({
        id: char.char_id,
        name: char.name,
        portrait: char.portrait,
        industryJobs: char.industryJobs,
        researchJobs: char.researchJobs,
        reactionJobs: char.reactionJobs,
        planetaryJobs: char.planetaryJobs,
      }));
    }

    return [];
  } catch (error) {
    console.error("Error fetching characters:", error);
    return [];
  }
};

export const fetchJobs = async () => {
  // For now, return empty array since we're focusing on character data
  // In the future, this would fetch actual job data from ESI
  return [];
};
