import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

export const api = axios.create({ baseURL: API });

export const getMenu = async () => {
  const { data } = await api.get('/menu');
  return data;
};

export const getSiteConfig = async () => {
  const { data } = await api.get('/site-config');
  return data;
};

export const adminLogin = async (password) => {
  const { data } = await api.post('/admin/login', { password });
  return data.token;
};

export const adminVerify = async (token) => {
  await api.get('/admin/verify', { headers: { Authorization: `Bearer ${token}` } });
};

export const adminUpdateMenu = async (token, menu) => {
  const { data } = await api.put('/admin/menu', menu, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return data;
};

export const adminUpdateSiteConfig = async (token, cfg) => {
  const { data } = await api.put('/admin/site-config', cfg, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return data;
};

export const adminUploadImage = async (token, file) => {
  const form = new FormData();
  form.append('file', file);
  const { data } = await api.post('/admin/upload', form, {
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'multipart/form-data',
    },
  });
  return data;
};

export const resolveAssetUrl = (u) => {
  if (!u) return '';
  if (u.startsWith('http://') || u.startsWith('https://')) return u;
  return `${BACKEND_URL}${u}`;
};
