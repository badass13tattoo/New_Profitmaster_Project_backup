// This module simulates a backend API.
// In the future, this would be replaced with actual HTTP fetch calls to the ESI or a custom backend.

const mockCharacters = [
  {
    id: 1,
    name: 'Jules The Engineer',
    portrait: 'https://images.evetech.net/characters/2112853242/portrait?size=64',
  },
  {
    id: 2,
    name: 'Another Pilot',
    portrait: 'https://images.evetech.net/characters/95465499/portrait?size=64',
  }
];

const mockJobs = [
    { id: 1, characterId: 1, name: 'Tritanium x300', type: 'Manufacturing', startDate: new Date(Date.now() - 2 * 3600 * 1000).toISOString(), endDate: new Date(Date.now() + 4 * 3600 * 1000).toISOString(), location: 'Jita IV-4', isPaused: false },
    { id: 2, characterId: 1, name: 'Isogen Research', type: 'Research', startDate: new Date(Date.now() + 1 * 3600 * 1000).toISOString(), endDate: new Date(Date.now() + 10 * 3600 * 1000).toISOString(), location: 'Rens VI-8', isPaused: true },
    { id: 3, characterId: 2, name: 'Water Planet Extraction', type: 'Planet Extraction', startDate: new Date(Date.now() - 6 * 3600 * 1000).toISOString(), endDate: new Date(Date.now() - 1 * 3600 * 1000).toISOString(), location: 'Amarr I', isPaused: false },
    { id: 4, characterId: 2, name: 'Oxygen Isotopes Reaction', type: 'Reaction', startDate: new Date(Date.now() + 3 * 3600 * 1000).toISOString(), endDate: new Date(Date.now() + 8 * 3600 * 1000).toISOString(), location: 'Dodixie IX-20', isPaused: false },
];

export const fetchCharacters = () => {
  return new Promise((resolve) => {
    setTimeout(() => resolve(mockCharacters), 200); // Simulate network delay
  });
};

export const fetchJobs = () => {
  return new Promise((resolve) => {
    setTimeout(() => resolve(mockJobs), 200); // Simulate network delay
  });
};