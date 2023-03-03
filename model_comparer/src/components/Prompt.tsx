import { PromptResults } from "../FileComparer";
import './Prompt.css';

interface PromptProps {
  prompt: string;
  results: PromptResults[];
  showSamplingMethod: boolean;
  outputIndex: number;
  showSamplingConfig: boolean;
  collapsed?: boolean;
  onToggleCollapsed?: () => void;
};

export const Prompt = ({collapsed, onToggleCollapsed, prompt, results, outputIndex, showSamplingMethod, showSamplingConfig}: PromptProps) => {
  return (
    <div>
      <div className="promptBubble" onClick={onToggleCollapsed}>{prompt}</div>
      { !collapsed &&
        <table className={showSamplingMethod ? 'replyTableWithAltRows' : ''}>
          <tbody>
            {results.map((result, modelIndex) => <tr key={result.file.model_name}>
              <td className="model_name">{result.file.model_name}</td>
              <td>{result.results.map((result, result_index) => (
                <div key={result_index}>
                  {showSamplingConfig && <div className="sampling_config">
                    {showSamplingMethod && <div>Sampling config: <b>{result.sampling_config}</b></div>}
                    {Object.keys(result.sampling_params).map(param => <div key={param}>{param}: <span className="param-value">{result.sampling_params[param].toString()}</span></div>)}
                  </div>}
                  {outputIndex === -1 ?
                    result.outputs.map((output, index) => <ReplyBubble key={index} modelIndex={modelIndex} output={output} saturation={result_index}/>) :
                    <ReplyBubble modelIndex={modelIndex} output={result.outputs[outputIndex]} saturation={result_index} />
                  }
                </div>
              ))}</td>
            </tr>)}
          </tbody>
        </table>
      }
    </div>
  );
}

const ReplyBubble = ({modelIndex, output, saturation} : { modelIndex: number, output: string, saturation: number }) => {
  return <div className="replyBubble" style={{background: `hsl(${194 + 42.3 * modelIndex} ${30 + 23 / (saturation + 1)}% ${73 + 10 / (saturation+1)}%)`}}>{output}</div>
}

