const editTweetSchema = [
    {
      $el: 'h3',
      children: 'Edit tweet'
    },
    {
      $formkit: 'textarea',
      name: 'tweet_content',
      label: 'Tweet',
      help: 'Edit the tweet.',
      validation: 'required|length:2,240'
    },
]
export default editTweetSchema