export interface TopicCluster {
  name: string;
  description: string;
  estimated_share: string;
  dominant_sentiment: 'positive' | 'neutral' | 'negative' | 'mixed';
}

export interface TopicClusteringPayload {
  topics: TopicCluster[];
}
