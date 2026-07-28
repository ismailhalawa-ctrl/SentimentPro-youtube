import * as React from 'react';

export interface FormFieldProps {
  label: string;
  htmlFor: string;
  error?: string;
  children: React.ReactNode;
}

function injectIntoFirstControl(node: React.ReactNode, props: Record<string, unknown>): React.ReactNode {
  if (!React.isValidElement(node)) return node;

  const element = node as React.ReactElement<{ children?: React.ReactNode }>;
  if (element.type !== 'div') {
    return React.cloneElement(element, props);
  }

  const childArray = React.Children.toArray(element.props.children);
  const targetIndex = childArray.findIndex(React.isValidElement);
  if (targetIndex === -1) return element;

  const newChildren = childArray.map((child, i) =>
    i === targetIndex ? injectIntoFirstControl(child, props) : child
  );

  return React.cloneElement(element, {}, newChildren);
}

export function FormField({ label, htmlFor, error, children }: FormFieldProps) {
  const errorId = `${htmlFor}-error`;

  const injected = injectIntoFirstControl(children, {
    id: htmlFor,
    'aria-invalid': !!error,
    'aria-describedby': error ? errorId : undefined,
  });

  return (
    <div className="flex flex-col gap-1.5">
      <label htmlFor={htmlFor} className="text-sm font-medium text-text-primary">
        {label}
      </label>
      {injected}
      {error && (
        <p id={errorId} role="alert" className="text-sm text-feedback-danger">
          {error}
        </p>
      )}
    </div>
  );
}
