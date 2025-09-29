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
    const response = await fetch(`${API_BASE_URL}/characters`);
    const data = await response.json();

    if (data.mode === "local" && data.characters) {
      // Generate mock job data based on character job indicators
      const jobs = [];
      const now = new Date();

      data.characters.forEach((char) => {
        const characterId = char.char_id;

        // Generate Industry jobs
        for (let i = 0; i < char.industryJobs.active; i++) {
          const startDate = new Date(
            now.getTime() - Math.random() * 24 * 60 * 60 * 1000
          ); // Random start within last 24h
          const endDate = new Date(
            startDate.getTime() + (2 + Math.random() * 6) * 60 * 60 * 1000
          ); // 2-8 hours duration

          jobs.push({
            id: `industry_${characterId}_${i}`,
            characterId: characterId,
            characterName: char.name,
            type: "industry",
            name: `Industry Job ${i + 1}`,
            startDate: startDate,
            endDate: endDate,
            status: endDate > now ? "active" : "completed",
            icon: "🏭",
          });
        }

        // Generate Research jobs
        for (let i = 0; i < char.researchJobs.active; i++) {
          const startDate = new Date(
            now.getTime() - Math.random() * 48 * 60 * 60 * 1000
          ); // Random start within last 48h
          const endDate = new Date(
            startDate.getTime() + (12 + Math.random() * 24) * 60 * 60 * 1000
          ); // 12-36 hours duration

          jobs.push({
            id: `research_${characterId}_${i}`,
            characterId: characterId,
            characterName: char.name,
            type: "research",
            name: `Research Job ${i + 1}`,
            startDate: startDate,
            endDate: endDate,
            status: endDate > now ? "active" : "completed",
            icon: "🔬",
          });
        }

        // Generate Reaction jobs
        for (let i = 0; i < char.reactionJobs.active; i++) {
          const startDate = new Date(
            now.getTime() - Math.random() * 12 * 60 * 60 * 1000
          ); // Random start within last 12h
          const endDate = new Date(
            startDate.getTime() + (1 + Math.random() * 3) * 60 * 60 * 1000
          ); // 1-4 hours duration

          jobs.push({
            id: `reaction_${characterId}_${i}`,
            characterId: characterId,
            characterName: char.name,
            type: "reaction",
            name: `Reaction Job ${i + 1}`,
            startDate: startDate,
            endDate: endDate,
            status: endDate > now ? "active" : "completed",
            icon: "⚗️",
          });
        }

        // Generate Planetary jobs
        for (let i = 0; i < char.planetaryJobs.active; i++) {
          const startDate = new Date(
            now.getTime() - Math.random() * 6 * 60 * 60 * 1000
          ); // Random start within last 6h
          const endDate = new Date(
            startDate.getTime() + (30 + Math.random() * 60) * 60 * 1000
          ); // 30-90 minutes duration

          jobs.push({
            id: `planetary_${characterId}_${i}`,
            characterId: characterId,
            characterName: char.name,
            type: "planetary",
            name: `Planetary Job ${i + 1}`,
            startDate: startDate,
            endDate: endDate,
            status: endDate > now ? "active" : "completed",
            icon: "🌍",
          });
        }
      });

      return jobs;
    }

    return [];
  } catch (error) {
    console.error("Error fetching jobs:", error);
    return [];
  }
};
