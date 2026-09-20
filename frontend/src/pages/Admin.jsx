import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  adminLogin,
  adminVerify,
  adminUpdateMenu,
  adminUpdateSiteConfig,
  adminUploadImage,
  getMenu,
  getSiteConfig,
  resolveAssetUrl,
} from '../lib/api';
import { Trash2, Plus, Upload, LogOut, Save, Loader2, Home, Eye } from 'lucide-react';

const TOKEN_KEY = 'vino_admin_token';
const CATEGORIES = ['fizz', 'white', 'orange', 'rose', 'red'];

const Admin = () => {
  const navigate = useNavigate();
  const [token, setToken] = useState(localStorage.getItem(TOKEN_KEY) || '');
  const [password, setPassword] = useState('');
  const [loginError, setLoginError] = useState('');
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [toast, setToast] = useState('');
  const [menu, setMenu] = useState(null);
  const [siteConfig, setSiteConfig] = useState(null);

  // Verify token on mount
  useEffect(() => {
    const check = async () => {
      if (!token) return;
      try {
        await adminVerify(token);
        loadData();
      } catch {
        localStorage.removeItem(TOKEN_KEY);
        setToken('');
      }
    };
    check();
    // eslint-disable-next-line
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [m, s] = await Promise.all([getMenu(), getSiteConfig()]);
      setMenu(m);
      setSiteConfig(s);
    } finally {
      setLoading(false);
    }
  };

  const showToast = (msg) => {
    setToast(msg);
    setTimeout(() => setToast(''), 2500);
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoginError('');
    setLoading(true);
    try {
      const t = await adminLogin(password);
      localStorage.setItem(TOKEN_KEY, t);
      setToken(t);
      await loadData();
    } catch (err) {
      setLoginError('Incorrect password');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem(TOKEN_KEY);
    setToken('');
    setMenu(null);
    setSiteConfig(null);
  };

  const handleUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    try {
      const { url } = await adminUploadImage(token, file);
      const updated = { ...siteConfig, hero_image_url: url };
      const saved = await adminUpdateSiteConfig(token, updated);
      setSiteConfig(saved);
      showToast('Header image updated');
    } catch (err) {
      showToast('Upload failed');
    } finally {
      setUploading(false);
      e.target.value = '';
    }
  };

  const handleSaveConfig = async () => {
    setSaving(true);
    try {
      const saved = await adminUpdateSiteConfig(token, siteConfig);
      setSiteConfig(saved);
      showToast('Hero settings saved');
    } finally {
      setSaving(false);
    }
  };

  const handleSaveMenu = async () => {
    setSaving(true);
    try {
      await adminUpdateMenu(token, menu);
      showToast('Wine list saved');
    } finally {
      setSaving(false);
    }
  };

  const updateItem = (cat, idx, field, value) => {
    setMenu((prev) => {
      const list = [...(prev[cat] || [])];
      list[idx] = { ...list[idx], [field]: value };
      return { ...prev, [cat]: list };
    });
  };

  const addItem = (cat) => {
    setMenu((prev) => ({
      ...prev,
      [cat]: [...(prev[cat] || []), { name: '', price: '' }],
    }));
  };

  const removeItem = (cat, idx) => {
    setMenu((prev) => ({
      ...prev,
      [cat]: prev[cat].filter((_, i) => i !== idx),
    }));
  };

  if (!token) {
    return (
      <div className="min-h-screen bg-foresta flex items-center justify-center px-6">
        <div className="w-full max-w-sm">
          <div className="text-center mb-10">
            <div className="vino-mono-medium text-bianco text-[10px] tracking-[0.5em] mb-3">MMXXV</div>
            <div className="vino-display text-bianco text-5xl tracking-[0.08em]">VINO</div>
            <div className="vino-script text-bianco text-2xl -mt-1">by tonino</div>
            <div className="vino-mono-medium text-ruggine text-[10px] tracking-[0.4em] mt-4">ADMIN</div>
          </div>
          <form onSubmit={handleLogin} className="space-y-4">
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              className="w-full bg-transparent border border-bianco/30 focus:border-bianco text-bianco vino-mono px-4 py-3 outline-none transition-colors placeholder:text-bianco/40"
              autoFocus
            />
            {loginError && (
              <div className="vino-mono text-ruggine text-[11px] tracking-wide">{loginError}</div>
            )}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-ruggine hover:bg-ruggine/85 text-bianco vino-mono-medium tracking-[0.3em] text-xs py-3 transition-colors disabled:opacity-60"
            >
              {loading ? 'SIGNING IN…' : 'SIGN IN'}
            </button>
            <button
              type="button"
              onClick={() => navigate('/')}
              className="w-full vino-mono text-bianco/60 hover:text-bianco text-[11px] tracking-[0.3em] py-2 transition-colors"
            >
              ← BACK TO SITE
            </button>
          </form>
        </div>
      </div>
    );
  }

  if (loading || !menu || !siteConfig) {
    return (
      <div className="min-h-screen bg-foresta flex items-center justify-center">
        <Loader2 className="text-bianco animate-spin" size={28} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-foresta text-bianco">
      {/* Top bar */}
      <div className="sticky top-0 z-30 bg-foresta/95 backdrop-blur border-b border-bianco/10">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-baseline gap-2">
            <span className="vino-display text-lg tracking-[0.3em]">VINO</span>
            <span className="vino-script text-lg">by tonino</span>
            <span className="vino-mono-medium text-ruggine text-[10px] tracking-[0.4em] ml-2">ADMIN</span>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => navigate('/')}
              className="vino-mono-medium text-[10px] tracking-[0.3em] px-3 py-2 border border-bianco/20 hover:border-bianco text-bianco/80 hover:text-bianco transition-colors flex items-center gap-2"
            >
              <Eye size={14} /> VIEW SITE
            </button>
            <button
              onClick={handleLogout}
              className="vino-mono-medium text-[10px] tracking-[0.3em] px-3 py-2 border border-bianco/20 hover:border-ruggine hover:text-ruggine text-bianco/80 transition-colors flex items-center gap-2"
            >
              <LogOut size={14} /> LOG OUT
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-10 space-y-12">
        {/* Header image section */}
        <section>
          <div className="flex items-baseline gap-3 mb-4">
            <div className="vino-mono-medium text-ruggine text-[10px] tracking-[0.4em]">01</div>
            <h2 className="vino-display text-2xl tracking-[0.15em]">HEADER IMAGE</h2>
          </div>
          <p className="vino-mono text-bianco/70 text-xs mb-6 max-w-2xl">
            Upload a new hero image (JPG/PNG/WEBP, up to 10MB). It will replace the image at the top of the site instantly.
          </p>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="relative aspect-[16/9] bg-black/40 overflow-hidden border border-bianco/10">
              {siteConfig.hero_image_url && (
                <img
                  src={resolveAssetUrl(siteConfig.hero_image_url)}
                  alt="Current hero"
                  className="w-full h-full object-cover"
                />
              )}
              <div className="absolute top-2 left-2 vino-mono-medium text-[9px] tracking-[0.35em] bg-foresta/80 px-2 py-1">
                CURRENT
              </div>
            </div>
            <div className="space-y-4">
              <label className="block">
                <div className="vino-mono-medium text-[10px] tracking-[0.35em] mb-2">UPLOAD NEW IMAGE</div>
                <div className="border border-dashed border-bianco/30 hover:border-ruggine transition-colors p-6 text-center cursor-pointer group">
                  <input
                    type="file"
                    accept="image/jpeg,image/png,image/webp"
                    onChange={handleUpload}
                    className="hidden"
                    disabled={uploading}
                  />
                  <div className="flex flex-col items-center gap-3 pointer-events-none">
                    {uploading ? (
                      <Loader2 className="animate-spin text-ruggine" size={28} />
                    ) : (
                      <Upload className="text-bianco group-hover:text-ruggine transition-colors" size={28} />
                    )}
                    <div className="vino-mono text-xs text-bianco/80">
                      {uploading ? 'Uploading…' : 'Click to select an image'}
                    </div>
                    <div className="vino-mono text-[10px] text-bianco/50">JPG, PNG, or WEBP · max 10MB</div>
                  </div>
                </div>
              </label>

              <div>
                <div className="vino-mono-medium text-[10px] tracking-[0.35em] mb-2">TAGLINE (SCRIPT)</div>
                <input
                  type="text"
                  value={siteConfig.hero_tagline || ''}
                  onChange={(e) =>
                    setSiteConfig({ ...siteConfig, hero_tagline: e.target.value })
                  }
                  className="w-full bg-transparent border border-bianco/25 focus:border-bianco text-bianco vino-mono px-3 py-2 outline-none transition-colors text-sm"
                />
              </div>

              <div>
                <div className="vino-mono-medium text-[10px] tracking-[0.35em] mb-2">YEAR BADGE</div>
                <input
                  type="text"
                  value={siteConfig.since_year || ''}
                  onChange={(e) =>
                    setSiteConfig({ ...siteConfig, since_year: e.target.value })
                  }
                  className="w-full bg-transparent border border-bianco/25 focus:border-bianco text-bianco vino-mono px-3 py-2 outline-none transition-colors text-sm"
                />
              </div>

              <button
                onClick={handleSaveConfig}
                disabled={saving}
                className="w-full bg-ruggine hover:bg-ruggine/85 text-bianco vino-mono-medium tracking-[0.3em] text-xs py-3 transition-colors flex items-center justify-center gap-2 disabled:opacity-60"
              >
                {saving ? <Loader2 size={14} className="animate-spin" /> : <Save size={14} />}
                SAVE HERO SETTINGS
              </button>
            </div>
          </div>
        </section>

        <div className="h-px bg-bianco/10" />

        {/* Menu section */}
        <section>
          <div className="flex items-baseline gap-3 mb-4">
            <div className="vino-mono-medium text-ruggine text-[10px] tracking-[0.4em]">02</div>
            <h2 className="vino-display text-2xl tracking-[0.15em]">WINE LIST</h2>
          </div>
          <p className="vino-mono text-bianco/70 text-xs mb-6 max-w-2xl">
            Add, edit, or remove wines under each category. Save when you're happy — changes appear on the public site instantly.
          </p>

          <div className="grid md:grid-cols-2 gap-x-10 gap-y-10">
            {CATEGORIES.map((cat) => (
              <div key={cat}>
                <div className="flex items-center justify-between mb-3">
                  <div className="vino-mono-medium text-bianco text-[11px] tracking-[0.4em] uppercase">
                    {cat}
                  </div>
                  <button
                    onClick={() => addItem(cat)}
                    className="vino-mono-medium text-[10px] tracking-[0.3em] text-ruggine hover:text-bianco transition-colors flex items-center gap-1"
                  >
                    <Plus size={12} /> ADD
                  </button>
                </div>
                <div className="space-y-2">
                  {(menu[cat] || []).map((item, idx) => (
                    <div key={idx} className="flex items-center gap-2">
                      <input
                        type="text"
                        value={item.name}
                        onChange={(e) => updateItem(cat, idx, 'name', e.target.value)}
                        placeholder="Wine name, region, country"
                        className="flex-1 bg-black/20 border border-bianco/15 focus:border-bianco text-bianco vino-mono text-[12px] px-3 py-2 outline-none transition-colors"
                      />
                      <input
                        type="text"
                        value={item.price}
                        onChange={(e) => updateItem(cat, idx, 'price', e.target.value)}
                        placeholder="28 / 5.5"
                        className="w-24 bg-black/20 border border-bianco/15 focus:border-bianco text-bianco vino-mono text-[12px] px-3 py-2 outline-none transition-colors text-right"
                      />
                      <button
                        onClick={() => removeItem(cat, idx)}
                        className="text-bianco/50 hover:text-ruggine transition-colors"
                        aria-label="Remove"
                      >
                        <Trash2 size={14} />
                      </button>
                    </div>
                  ))}
                  {(!menu[cat] || menu[cat].length === 0) && (
                    <div className="vino-mono text-bianco/40 text-[11px] italic">No items yet.</div>
                  )}
                </div>
              </div>
            ))}
          </div>

          <div className="mt-10 flex justify-end">
            <button
              onClick={handleSaveMenu}
              disabled={saving}
              className="bg-ruggine hover:bg-ruggine/85 text-bianco vino-mono-medium tracking-[0.3em] text-xs px-6 py-3 transition-colors flex items-center gap-2 disabled:opacity-60"
            >
              {saving ? <Loader2 size={14} className="animate-spin" /> : <Save size={14} />}
              SAVE WINE LIST
            </button>
          </div>
        </section>
      </div>

      {/* Toast */}
      <div
        className={`fixed bottom-6 left-1/2 -translate-x-1/2 z-50 transition-all duration-300 ${
          toast ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4 pointer-events-none'
        }`}
      >
        <div className="bg-bianco text-foresta vino-mono-medium text-[11px] tracking-[0.3em] px-5 py-3 shadow-lg">
          {toast}
        </div>
      </div>
    </div>
  );
};

export default Admin;
