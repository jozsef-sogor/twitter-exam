const forgotPasswordSchema = [
    {
      $el: 'h3',
      children: 'Forgot password'
    },
    {
      $formkit: 'email',
      name: 'user_email',
      label: 'Email',
      help: 'Email address associated with your account',
      validation: 'required'
    },
]
export default forgotPasswordSchema