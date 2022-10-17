export const useLorem = () => {
  const { data } = useFetch(
    "https://loripsum.net/api/1/short/plaintext"
  ).text();
  return data;
};
