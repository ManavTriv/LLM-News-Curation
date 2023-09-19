import 'tailwindcss/tailwind.css';
import Head from 'next/head';
import Navbar from '@/components/Navbar';
import { useRouter } from 'next/router';

function Index() {
  const router = useRouter();

  const ArticleSearch = () => {
    router.push('/articleSearch');
  };

  const ProfileSearch = () => {
    router.push('/profileSearch')
  };

  const ArticleLine = ({text}) => {

    return (
      <div className='flex flex-col items-center justify-center w-6'>
        <div style={{ display: "flex", alignItems: "center", width: "2px"}}>
          <div style={{ flex: 1, backgroundColor: "#7895B1", height: "92px" }} />
        </div>
        <span className='-rotate-90 text-[#7895B1] text-xs font-bold w-20 mt-1'>ARTICLE</span>
        <div className="mt-9" style={{ display: "flex", alignItems: "center", width: "2px"}}>
          <div style={{ flex: 1, backgroundColor: "#7895B1", height: "92px" }} />
        </div>
      </div>
    )
  }

  const ProfileLine = ({text}) => {

    return (
      <div className='flex flex-col items-center justify-center w-6'>
        <div style={{ display: "flex", alignItems: "center", width: "2px"}}>
          <div style={{ flex: 1, backgroundColor: "#7895B1", height: "92px" }} />
        </div>
        <span className='rotate-90 text-[#7895B1] text-xs font-bold mt-5'>PROFILE</span>
        <div className="mt-5" style={{ display: "flex", alignItems: "center", width: "2px"}}>
          <div style={{ flex: 1, backgroundColor: "#7895B1", height: "92px" }} />
        </div>
      </div>
    )
  }


  return (
    <div>
      <Head>
        <title>Just The Facts</title>
      </Head>
      <Navbar />
      <div className='min-h-screen bg-[#5F7A95]'>
        <div className='hero'>
          <div className='hero-content p'>
            <div>
              <div className="mt"style={{ width: '1000px'}}><text className="text-white font-bold text-xl">
                                <text className="text-[#FFB039] font-extrabold">JUST THE FACTS</text> lets you discover unbiased
                            political insights. <text className="text-[#FFB039] font-extrabold">START</text> by either filtering through a 
                            <text className="font-extrabold"> single article</text> or by exploring impartial
                            <text className="font-extrabold"> political profiles</text> containing a collection of articles.</text>
                </div>

              <div className='flex justify-center space-x-20 mt-14'>

                <div>
                  <div className='flex'>
                    <div className='flex items-center justify-center '>
                      <ArticleLine text={"ARTICLE"}/>
                    </div>
                    <div
                      className='card bg-[#7895B1] rounded-lg '
                      style={{ width: '370px', height: '250px' }}
                    >
                      <button
                        className='btn btn-sm btn-neutral bg-[#2E2E2E] rounded-xl mt-48 ml-10'
                        style={{ width: '285px', height: '35px' }}
                        onClick={ArticleSearch}
                      >
                        <text className='text-white text-sm'>CLICK HERE FOR ARTICLE SEARCH</text>
                      </button>
                    </div>
                  </div>
                </div>

                <div>
                  <div className='flex'>
                    <div
                      className='card bg-[#7895B1] rounded-lg'
                      style={{ width: '370px', height: '250px' }}
                    >
                      <button
                        className='btn btn-sm btn-neutral bg-[#2E2E2E] rounded-xl mt-48 ml-10'
                        style={{ width: '285px', height: '35px' }}
                        onClick={ProfileSearch}
                      >
                        <text className='text-white text-sm'>CLICK HERE FOR PROFILE SEARCH</text>
                      </button>
                    </div>
                    <div className='flex items-center justify-center '>
                      <ProfileLine text={"Profile"}/>
                    </div>
                  </div>
                </div>

              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Index;
