import Image from 'next/image';
import Clipboard from './pictures/clipboard.png';
import { sendSaveArticle } from '@/utils/sendSaveArticle';

/**
 * Card is a the componenet that displays the main body of the article search and analysis page
 *
 * @component
 * @param {string} title - The title of the article
 * @param {string} content - The contents of the article
 * @param {boolean} highlight - Indicates if highlighting is enabled.
 * @param {Object} biasWords - A dictionary of bias words for highlighting.
 * @param {string} url - The URL of the article.
 * @returns {JSX.Element} A React JSX element representing the card.
 */
const Card = ({ title, content, highlight = false, biasWords, url }) => {
  let phrases = [];
  let keys = [];
  let dotPoints = null;

  // Split content into phrases for highlighting
  if (highlight && content && biasWords) {
    keys = Object.keys(biasWords);
    phrases = content.split(new RegExp(`(${keys.join('|')})`, 'gi'));
  }
  // Function to copy content to clipboard
  const copy = () => {
    navigator.clipboard.writeText(content);
  };

  if (typeof content === 'string') {
    dotPoints = content.split('\n');
  }

  // Function to save the article
  const save = () => {
    sendSaveArticle(url);
  };

  return (
    <div className='card bg-white shadow-xl flex flex-col'>
      <div className='card-body text-black'>
        <div className='p'>
          <div className='card-title flex justify-center font-bold text-4xl text-gray-600'>
            {title}
          </div>
          {highlight && biasWords ? (
            phrases.map((phrase, index) => {
              const matches = keys.find(
                (key) => phrase.toLowerCase() === key.toLowerCase()
              );

              const isHighlighted = !!matches;
              const phraseKey = `${phrase}-${index}`;
              return isHighlighted ? (
                <div
                  className='tooltip tooltip-bottom'
                  data-tip={biasWords[phrase]}
                >
                  <span key={phraseKey} className='bg-red-300'>
                    {phrase}{' '}
                  </span>
                </div>
              ) : (
                <span key={phraseKey}>{phrase} </span>
              );
            })
          ) : dotPoints ? (
            dotPoints.map((point, index) => <p key={index}>{point}</p>)
          ) : (
            <>{content}</>
          )}
        </div>

        <div className='flex flex-row items-center space-x-6 mt-6'>
          <button
            onClick={copy}
            className='btn btn-xs btn-neutral bg-[#2E2E2E] rounded-full text-white font-semibold'
          >
            <Image src={Clipboard} width={13} height={13} />
            COPY TO CLIPBOARD
          </button>
          <button
            onClick={save}
            className='btn btn-xs btn-neutral bg-[#2E2E2E] rounded-full text-white font-semibold'
          >
            + SAVE PAGE SEARCH
          </button>
        </div>
      </div>
    </div>
  );
};

export default Card;
