export type RenderProps = {
  compositionId: string;
  jobId: string;
  language: {
    code: string;
    label: string;
  };
  platforms: string[];
  video: {
    width: number;
    height: number;
    fps: number;
    durationInFrames: number;
  };
  theme: {
    brandLabel: string;
    badge: string;
    fontFamily: string;
    start: string;
    end: string;
    accent: string;
  };
  hook: {
    title: string;
    support: string;
    cta: string;
    keywords: string[];
    visualMotifs: string[];
    traits: string[];
  };
  captions: string[];
  narration: {
    audioSrc: string | null;
    durationSeconds: number;
    voice: string;
  };
};
