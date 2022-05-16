const loginSchema = [
    {
      $el: 'h3',
      children: 'Login'
    },
    {
      $formkit: 'text',
      name: 'user_email',
      label: 'Email',
      help: 'This will be used for your account.',
      validation: 'required|email'
    },
    {
      $formkit: 'password',
      name: 'user_password',
      label: 'Password',
      help: 'Enter your new password.',
      validation: 'required|length:3,120'
    },
]

export default loginSchema