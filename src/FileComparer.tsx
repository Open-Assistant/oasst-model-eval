import { useMemo, useState } from "react";
import { JsonFile, JsonFilePrompt } from "./Comparer";
import './FileComparer.css'

interface PromptResults {
  file: JsonFile;
  results: JsonFilePrompt[]
}

export const FileComparer = ({files}: {files:JsonFile[]}) => {
  const samplingMethods = useMemo(() => {
    const s = new Set<string>();
    files.forEach(file => file.prompts?.forEach(p => p.results.forEach(result => s.add(result.sampling_config))));
    return Array.from(s.values());
  }, [files]);

  const [samplingMethod, setSamplingMethod] = useState<string>(samplingMethods[0] || 'beam5');
  const [outputIndex, setOutputIndex] = useState<number>(0); // -1 for all

  const prompts = useMemo(() => {
    const prompts: {[prompt: string]: PromptResults[]} = {};
    files.forEach(file => {
      file.prompts?.forEach(p => {
        if (!prompts[p.prompt]) {
          prompts[p.prompt] = [];
        }
        prompts[p.prompt] = [...prompts[p.prompt], {file, results: p.results.filter(r => !samplingMethod || (r.sampling_config === samplingMethod))}];
      });
    });
    return prompts;
  }, [files, samplingMethod]);

  return (
    <div>
      <div className="config_options">
        <div>
          <label htmlFor="samplingMethod">Sampling Method: &nbsp;</label>
          <select id="samplingMethod" value={samplingMethod} onChange={(e) => setSamplingMethod(e.target.value)}>
            <option value="">Show all</option>
            {samplingMethods.map(s => <option key={s} value={s}>{s}</option>)}
          </select>
        </div>
        <div>
          <label htmlFor="outputIndex">Output Index: &nbsp;</label>
          <select id="outputIndex" value={outputIndex} onChange={(e) => setOutputIndex(parseInt(e.target.value))}>
            <option value={-1}>Show all</option>
            <option value={0}>0</option>
            <option value={1}>1</option>
          </select>
        </div>
      </div>
      {Object.keys(prompts).map((p) => <Prompt key={p} prompt={p} results={prompts[p]} outputIndex={outputIndex} showSamplingMethod={samplingMethod === ''}/>)}
    </div>
  );
}

interface PromptProps {
  prompt: string;
  results: PromptResults[];
  showSamplingMethod: boolean;
  outputIndex: number;
};

export const Prompt = ({prompt, results, outputIndex, showSamplingMethod}: PromptProps) => {
  return (
    <div>
      <div className="promptBubble">{prompt}</div>
      <table>
        <tbody>
          {results.map(result => <tr key={result.file.model_name}>
            <td className="model_name">{result.file.model_name}</td>
            <td>{result.results.map((result, result_index) => (
              <div key={result_index}>
              <div className="sampling_config">
                {showSamplingMethod && <div>Sampling config: {result.sampling_config}</div>}
                {Object.keys(result.sampling_params).map(param => <div key={param}>{param}: {result.sampling_params[param].toString()}</div>)}
              </div>
              {outputIndex === -1 ?
                result.outputs.map((output, index) => <div key={index} className="replyBubble">{output}</div>) :
                <div className="replyBubble">{result.outputs[outputIndex]}</div>
              }
              </div>
            ))}</td>
          </tr>)}
        </tbody>
      </table>
    </div>
  );
}
