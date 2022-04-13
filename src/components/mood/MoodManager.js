export const getMoods = () => {
  return fetch("http://localhost:8085/moods")
    .then(res => res.json())
};
