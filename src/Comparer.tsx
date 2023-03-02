import React, { useEffect, useState } from 'react';
import './Comparer.css';
import { FileComparer } from './FileComparer';

export interface JsonFilePrompt {
  outputs: string[];
  sampling_config: string;
  sampling_params: {[key: string]: string | number | boolean};
}

export interface JsonFile {
  model_name: string;
  date: string;
  args: {[key: string]: any};
  prompts: {prompt: string, results: JsonFilePrompt[]}[];
}

const someUrls = `https://raw.githubusercontent.com/LAION-AI/Open-Assistant/main/model/model_eval/manual/sampling_reports/2023-03-01_theblackcat102_pythia-12b-deduped-sft_sampling.json
https://raw.githubusercontent.com/LAION-AI/Open-Assistant/main/model/model_eval/manual/sampling_reports/2023-03-01_theblackcat102_pythia-1b-deduped-sft_sampling.json
https://raw.githubusercontent.com/LAION-AI/Open-Assistant/main/model/model_eval/manual/sampling_reports/2023-03-01_theblackcat102_pythia-3b-deduped-sft_sampling.json`;

const fileCache: {[key:string]:JsonFile } = {}

async function catchedFetch(url: string) {
  if (fileCache[url]) {
    return fileCache[url];
  }
  return await fetch(url).then(r => r.json()).then(json => {
    fileCache[url] = json;
    return json;
  });
}

export const Comparer = () => {
  const [filenamesTxt, setFilenamesTxt] = useState<string>(localStorage.getItem('filesnames') || someUrls);
  const [files, setFiles] = useState<JsonFile[]>([]);
  const [fileErrors, setFileErrors] = useState<string[]>([]);
  const [loading, setLoading] = useState<number>(0);

  useEffect(() => {
    localStorage.setItem('filenames', filenamesTxt);
  }, [filenamesTxt]);

  useEffect(() => {
    const urls = filenamesTxt.split(/[\r\n]/).map(s => s.trim()).filter(s => s);
    setLoading(urls.length);
    setFileErrors([]);
    setFiles([]);
    urls.forEach((url, index) => catchedFetch(url).then(json => {
      setFiles(fs => {
        const fs_ = [...fs];
        fs_[index] = json;
        return fs_;
      });
      setFileErrors(es => { const es_ = [...es]; es_[index] = ''; return es_});
    }).catch(e => {
      setFileErrors(es => { const es_ = [...es]; es_[index] = `Failed to load ${url}: ${e.toString()}`; return es_});
    }).finally(() => setLoading(l => l - 1)));
  }, [filenamesTxt]);

  return (
    <div className="comparer">
      <h1>Model Output Comparer</h1>
      <div className={loading > 0 ? "loading_wait" : fileErrors.some(e => e) ? "loading_errors" : "loading_success"}>
        <textarea className="filenames" placeholder="Enter url to json file or drag and drop files in" value={filenamesTxt} onChange={(e) => setFilenamesTxt(e.target.value)} />
      </div>
      {loading > 0 && <div className="loading">Loading... ({loading} more)</div>}
      <div className="errors">{fileErrors.map((e, i) => e && <div className="error" key={i}>{e}</div>)}</div>
      <FileComparer files={files} />
    </div>
  );
}
