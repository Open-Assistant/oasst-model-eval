import { PromptResults } from "../FileComparer";

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
