export interface FAQEntry {
  question: string;
  answer: string;
  times_asked_estimate: number;
}

export interface FAQPayload {
  faqs: FAQEntry[];
}
