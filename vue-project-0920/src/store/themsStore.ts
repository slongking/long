// useStorage.js
import { ref, watch } from 'vue';

export function useStorage(key:any, defaultValue:any) {
  const getStorageValue = () => {
    const value = localStorage.getItem(key);
    return value !== null ? JSON.parse(value) : defaultValue;
  };

  const setStorageValue = (value:any) => {
    localStorage.setItem(key, JSON.stringify(value));
  };

  const storageValue = ref(getStorageValue());

  watch(storageValue, (newValue) => {
    setStorageValue(newValue);
  });

  return storageValue;
}