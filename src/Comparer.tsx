import React, { useEffect, useState } from 'react';
import { Octokit } from "octokit";
import './Comparer.css';
import { FileComparer } from './FileComparer';

const octokit = new Octokit();

interface GithubFileEntryType {
  download_url: string;
  name: string;
  type: "file" | "dir";
}

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

export const Comparer = () => {
  const [url, setUrl] = useState<string>('/repos/LAION-AI/Open-Assistant/contents/model/model_eval/manual/sampling_reports');
  const [filenames, setFilenames] = useState<GithubFileEntryType[]>([]);
  const [files, setFiles] = useState<JsonFile[]>([]);

  useEffect(() => {
    // https://github.com/LAION-AI/Open-Assistant/tree/main/model/model_eval/manual/sampling_reports
    setFilenames([]);
    octokit.request(url, {
      owner: 'OWNER',
      repo: 'REPO',
      path: 'PATH'
    }).then( filenames => setFilenames((filenames.data as GithubFileEntryType[]).filter(f => f.type ==='file')));
  }, [url]);

  useEffect(() => {
    filenames.forEach((f, index) => {
      octokit.request(f.download_url).then( file => setFiles(files => {
        const files_ = [...files];
        files_[index] = JSON.parse(file.data) as JsonFile;
        return files_;
      }));
    });
  }, [filenames]);

  return (
    <div className="comparer">
      <h1>Model Output Comparer - Loads from GitHub</h1>
      <input value={url} onChange={(e) => setUrl(e.target.value)} />
      <ul className="filelist">
        {filenames.map(f => <li key={f.name}>{f.name}</li>)}
      </ul>
      <FileComparer files={files} />
    </div>
  );
}
