import hooks from 'eslint-plugin-react-hooks';
import globals from 'globals';
export default [{
  files: ['src/**/*.{js,jsx}'],
  languageOptions: {ecmaVersion: 'latest', sourceType: 'module', parserOptions: {ecmaFeatures: {jsx: true}}, globals: {...globals.browser, ...globals.node}},
  plugins: {'react-hooks': hooks},
  rules: {'react-hooks/rules-of-hooks': 'error'},
}];
