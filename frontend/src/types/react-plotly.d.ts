// declare module 'react-plotly.js' {
//     import * as Plotly from 'plotly.js';
//     import * as React from 'react';

//     export interface PlotParams {
//         data: Plotly.Data[];
//         layout: Partial<Plotly.Layout>;
//         config?: Partial<Plotly.Config>;
//         onInitialized?: (figure: Readonly<Plotly.Figure>, graphDiv: HTMLElement) => void;
//         onUpdate?: (figure: Readonly<Plotly.Figure>, graphDiv: HTMLElement) => void;
//         onPurge?: (component: Component<PlotParams>, graphDiv: HTMLElement) => void;
//         onError?: (error: Error) => void;
//         style?: React.CSSProperties;
//         className?: string;
//         useResizeHandler?: boolean;
//         debug?: boolean;
//     }

//     export default class Plot extends React.Component<PlotParams> {}
// }

// export { Plot };