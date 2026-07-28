export function staggerContainer(staggerChildren = 0.08) {
  return {
    hidden: {},
    visible: { transition: { staggerChildren } },
  };
}

export const fadeUpItem = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};