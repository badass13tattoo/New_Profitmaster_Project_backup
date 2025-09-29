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
  try {
    const response = await fetch(`${API_BASE_URL}/jobs`);
    const data = await response.json();

    if (data.mode === "local" && data.jobs) {
      // Transform the job data to match the expected format
      return data.jobs.map((job) => ({
        id: job.id,
        characterId: job.characterId,
        characterName: job.characterName,
        type: job.type,
        name: job.name,
        startDate: new Date(job.startDate),
        endDate: new Date(job.endDate),
        status: job.status,
        icon: job.icon,
        location: job.location,
        blueprint: job.blueprint,
        runs: job.runs,
        progress: job.progress,
      }));
    }

    return [];
  } catch (error) {
    console.error("Error fetching jobs:", error);
    return [];
  }
};
